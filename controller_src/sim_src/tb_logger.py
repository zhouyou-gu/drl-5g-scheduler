#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import csv
import fnmatch
import os
import pprint
from io import StringIO
from threading import Lock

import matplotlib.pyplot as plt
import six
from tensorboard.backend.event_processing import event_accumulator
from torch.utils.tensorboard import SummaryWriter

from sim_src.util import *

TMP_LOG_PATH = "/tmp/"


def string_to_tb_string(markdown_string):
    if isinstance(markdown_string, six.binary_type):
        markdown_string = markdown_string.decode('utf-8')
    markdown_string = markdown_string.replace('\n', '  \n')
    markdown_string = markdown_string.replace('\t', '    ')
    return markdown_string


def plot_cdf(mat, fig_size=(10, 8)):
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111)
    n = mat.shape[0] // 10
    for y in range(mat.shape[1]):
        p, x = np.histogram(mat[:, y], bins=n)
        x = x[:-1] + (x[1] - x[0]) / 2
        ax.plot(x, np.cumsum(p / mat.shape[0]))
    ax.set_xlabel('Accuracy', fontsize=10)
    ax.set_ylabel('CDF', fontsize=10)
    ax.grid()
    fig.tight_layout()
    return fig


class MyPrettyPrinter(pprint.PrettyPrinter):
    def format_namedtuple(self, object, stream, indent, allowance, context, level):
        # Code almost equal to _format_dict, see pprint code
        write = stream.write
        write(object.__class__.__name__ + '(')
        object_dict = object._asdict()
        length = len(object_dict)
        if length:
            # We first try to print inline, and if it is too large then we print it on multiple lines
            inline_stream = StringIO()
            self.format_namedtuple_items(object_dict.items(), inline_stream, indent, allowance + 1, context, level,
                                         inline=True)
            max_width = self._width - indent - allowance
            if len(inline_stream.getvalue()) > max_width:
                self.format_namedtuple_items(object_dict.items(), stream, indent, allowance + 1, context, level,
                                             inline=False)
            else:
                stream.write(inline_stream.getvalue())
        write(')')

    def format_namedtuple_items(self, items, stream, indent, allowance, context, level, inline=False):
        # Code almost equal to _format_dict_items, see pprint code
        indent += self._indent_per_level
        write = stream.write
        last_index = len(items) - 1
        if inline:
            delimnl = ', '
        else:
            delimnl = ',\n' + ' ' * indent
            write('\n' + ' ' * indent)
        for i, (key, ent) in enumerate(items):
            last = i == last_index
            write(key + '=')
            self._format(ent, stream, indent + len(key) + 2,
                         allowance if last else 1,
                         context, level)
            if not last:
                write(delimnl)

    def _format(self, object, stream, indent, allowance, context, level):
        # We dynamically add the types of our namedtuple and namedtuple like
        # classes to the _dispatch object of pprint that maps classes to
        # formatting methods
        # We use a simple criteria (_asdict method) that allows us to use the
        # same formatting on other classes but a more precise one is possible
        if hasattr(object, '_asdict') and type(object).__repr__ not in self._dispatch:
            self._dispatch[type(object).__repr__] = MyPrettyPrinter.format_namedtuple
        super(MyPrettyPrinter, self)._format(object, stream, indent, allowance, context, level)


NAMETUPLE_PRINTER = MyPrettyPrinter(indent=2, depth=10)


class MySummaryWriter(SummaryWriter):
    scalar_filter_list = None

    def add_text(self, tag, text_string, global_step=None, walltime=None):
        text_string = string_to_tb_string(text_string)
        SummaryWriter.add_text(self, tag, text_string, global_step=global_step, walltime=walltime)

    def add_text_of_object(self, tag, object, global_step=None, walltime=None):
        text_string = NAMETUPLE_PRINTER.pformat(object)
        print(text_string)
        text_string = string_to_tb_string(text_string)
        SummaryWriter.add_text(self, tag, text_string, global_step=global_step, walltime=walltime)

    def set_scalar_filter(self, scalar_filter_list):
        self.scalar_filter_list = scalar_filter_list

    def add_scalar(self, tag, scalar_value, global_step=None, walltime=None):
        if self.scalar_filter_list is None:
            SummaryWriter.add_scalar(self, tag, scalar_value, global_step=global_step, walltime=walltime)
        elif any(s in tag for s in self.scalar_filter_list):
            SummaryWriter.add_scalar(self, tag, scalar_value, global_step=global_step, walltime=walltime)


class LearningLogger():
    def __init__(self):
        self.__tb_logger_is_set = False
        self.__tb_logger = None

        self.__path_folder = None
        self.__exp_name = None
        self.__lock = Lock()

        self.set_log_path(TMP_LOG_PATH, 'test', 'test')

    def set_log_path(self, path, log_folder_name, experiment_name):
        assert os.path.exists(path)
        assert os.access(os.path.dirname(path), os.W_OK)
        assert isinstance(log_folder_name, str)
        assert isinstance(experiment_name, str)

        self.__path_folder = os.path.join(path, log_folder_name, experiment_name + "-" + get_current_time_str())
        self.__exp_name = experiment_name
        self.__tb_logger = MySummaryWriter(log_dir=self.__path_folder, filename_suffix="." + experiment_name)
        self.__tb_logger_is_set = True

    def get_tb_logger(self) -> MySummaryWriter:
        '''
        example
             GLOBAL_LOGGER.get_tb_logger().add_scalar('rlc_r'+str(self.id), self.n_step,self.n_step)
        :return: the global summary writer
        '''
        assert self.__tb_logger is None or self.__tb_logger_is_set is True, "Set log path first"
        return self.__tb_logger

    def close_logger(self):
        assert self.__tb_logger is None or self.__tb_logger_is_set is True, "Set log path first"
        self.__tb_logger.close()

    def get_log_path(self):
        return self.__path_folder + '/'

    def reset_event_file(self):
        sl = None
        if self.__tb_logger_is_set:
            sl = self.__tb_logger.scalar_filter_list
        self.__tb_logger = MySummaryWriter(log_dir=self.__path_folder, filename_suffix="." + self.__exp_name)
        self.__tb_logger.set_scalar_filter(sl)
        self.__tb_logger_is_set = True


GLOBAL_LOGGER = LearningLogger()


class TBScalarToCSV():
    def __init__(self, events_out_path, csv_out_path, list_of_scalar_name: list):
        self.events_out_path = events_out_path
        self.csv_out_path = csv_out_path
        self.list_of_scalar_name = list_of_scalar_name
        assert isinstance(list_of_scalar_name, list), 'add a list of the scalar name'
        print(self.list_of_scalar_name)

        # for path, dirs, files in os.walk(self.events_out_path):
        # 	for filename in files:
        # 		if fnmatch.fnmatch(filename, 'events.out*'):
        # 			print(filename)
        # path_to_file = os.path.join(self.events_out_path,filename)
        SIZE_GUIDANCE = {
            event_accumulator.COMPRESSED_HISTOGRAMS: 500,
            event_accumulator.IMAGES: 4,
            event_accumulator.AUDIO: 4,
            event_accumulator.SCALARS: 0,
            event_accumulator.HISTOGRAMS: 1,
            event_accumulator.TENSORS: 10,
        }
        ea = event_accumulator.EventAccumulator(self.events_out_path, size_guidance=SIZE_GUIDANCE)
        path_to_dir = os.path.join(self.csv_out_path, 'csv')
        self._export_get_scalers(ea, path_to_dir)

    def _export_get_scalers(self, ea, to_dir):
        ea.Reload()
        print('Reload', ea.Tags())
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)

        for ss in ea.Tags()['scalars']:
            # for ss in self.list_of_scalar_name:
            if any(s in ss for s in self.list_of_scalar_name):
                path_to_file = os.path.join(to_dir, ss + '.csv')
                with open(path_to_file, 'w') as file:
                    w = csv.writer(file, delimiter=',')
                    w.writerows([(str(step.wall_time), str(step.step), str(step.value)) for step in ea.Scalars(ss)])


class TBTextToConfig():
    def __init__(self, events_out_path, config_out_path):
        self.events_out_path = events_out_path
        self.config_out_path = config_out_path

        for path, dirs, files in os.walk(self.events_out_path):
            for filename in files:
                if fnmatch.fnmatch(filename, 'events.out*'):
                    print(filename)
                    path_to_file = os.path.join(path, filename)
                    SIZE_GUIDANCE = {
                        event_accumulator.COMPRESSED_HISTOGRAMS: 500,
                        event_accumulator.IMAGES: 4,
                        event_accumulator.AUDIO: 4,
                        event_accumulator.SCALARS: 1,
                        event_accumulator.HISTOGRAMS: 1,
                        event_accumulator.TENSORS: 0,
                    }
                    ea = event_accumulator.EventAccumulator(path_to_file, size_guidance=SIZE_GUIDANCE)
                    path_to_dir = os.path.join(config_out_path, 'config')
                    self._export_text(ea, path_to_dir)

    def _export_text(self, ea, to_dir):
        ea.Reload()
        print('Reload', ea)
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)

        for s in ea.Tags()['tensors']:
            if '/text_summary' in s:
                config_name = s.replace('/text_summary', '')
                path_to_file = os.path.join(to_dir, config_name + '.config')
                with open(path_to_file, 'w') as file:
                    for i in range(len(ea.Tensors(s))):
                        for ii in range(len(ea.Tensors(s)[i].tensor_proto.string_val)):
                            config_string = ea.Tensors(s)[i].tensor_proto.string_val[ii].decode('utf-8')
                            print(config_string)
                            file.write(config_string)


if __name__ == '__main__':

    for filename in os.listdir('.'):
        if fnmatch.fnmatch(filename, '*.py'):
            print(filename)
    # path = root.split(os.sep)
    # print((len(path) - 1) * '---', os.path.basename(root))
    # for file in files:
    # 	print(len(path) * '---', file)

    GLOBAL_LOGGER.set_log_path(TMP_LOG_PATH, "hello/", "test")
    # GLOBAL_LOGGER.get_tb_logger().set_scalar_filter(['hi'])

    GLOBAL_LOGGER.get_tb_logger().add_text("hi", "hi 5", 3)
    GLOBAL_LOGGER.get_tb_logger().add_scalar("hidfaas", 3)
    GLOBAL_LOGGER.get_tb_logger().add_scalar("aaa", 3)
    GLOBAL_LOGGER.close_logger()
