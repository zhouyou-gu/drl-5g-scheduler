// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: nn_config.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_nn_5fconfig_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_nn_5fconfig_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3012000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3012004 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_nn_5fconfig_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_nn_5fconfig_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_nn_5fconfig_2eproto;
namespace ddrl {
class nn_config;
class nn_configDefaultTypeInternal;
extern nn_configDefaultTypeInternal _nn_config_default_instance_;
}  // namespace ddrl
PROTOBUF_NAMESPACE_OPEN
template<> ::ddrl::nn_config* Arena::CreateMaybeMessage<::ddrl::nn_config>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace ddrl {

enum nn_config_af_type : int {
  nn_config_af_type_NONE = 0,
  nn_config_af_type_RELU = 1,
  nn_config_af_type_SIGMOID = 2,
  nn_config_af_type_TANH = 3,
  nn_config_af_type_nn_config_af_type_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<::PROTOBUF_NAMESPACE_ID::int32>::min(),
  nn_config_af_type_nn_config_af_type_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<::PROTOBUF_NAMESPACE_ID::int32>::max()
};
bool nn_config_af_type_IsValid(int value);
constexpr nn_config_af_type nn_config_af_type_af_type_MIN = nn_config_af_type_NONE;
constexpr nn_config_af_type nn_config_af_type_af_type_MAX = nn_config_af_type_TANH;
constexpr int nn_config_af_type_af_type_ARRAYSIZE = nn_config_af_type_af_type_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* nn_config_af_type_descriptor();
template<typename T>
inline const std::string& nn_config_af_type_Name(T enum_t_value) {
  static_assert(::std::is_same<T, nn_config_af_type>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function nn_config_af_type_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    nn_config_af_type_descriptor(), enum_t_value);
}
inline bool nn_config_af_type_Parse(
    const std::string& name, nn_config_af_type* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<nn_config_af_type>(
    nn_config_af_type_descriptor(), name, value);
}
// ===================================================================

class nn_config PROTOBUF_FINAL :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:ddrl.nn_config) */ {
 public:
  inline nn_config() : nn_config(nullptr) {};
  virtual ~nn_config();

  nn_config(const nn_config& from);
  nn_config(nn_config&& from) noexcept
    : nn_config() {
    *this = ::std::move(from);
  }

  inline nn_config& operator=(const nn_config& from) {
    CopyFrom(from);
    return *this;
  }
  inline nn_config& operator=(nn_config&& from) noexcept {
    if (GetArena() == from.GetArena()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const nn_config& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const nn_config* internal_default_instance() {
    return reinterpret_cast<const nn_config*>(
               &_nn_config_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(nn_config& a, nn_config& b) {
    a.Swap(&b);
  }
  inline void Swap(nn_config* other) {
    if (other == this) return;
    if (GetArena() == other->GetArena()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(nn_config* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArena() == other->GetArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline nn_config* New() const final {
    return CreateMaybeMessage<nn_config>(nullptr);
  }

  nn_config* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<nn_config>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const nn_config& from);
  void MergeFrom(const nn_config& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  ::PROTOBUF_NAMESPACE_ID::uint8* _InternalSerialize(
      ::PROTOBUF_NAMESPACE_ID::uint8* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(nn_config* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "ddrl.nn_config";
  }
  protected:
  explicit nn_config(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_nn_5fconfig_2eproto);
    return ::descriptor_table_nn_5fconfig_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  typedef nn_config_af_type af_type;
  static constexpr af_type NONE =
    nn_config_af_type_NONE;
  static constexpr af_type RELU =
    nn_config_af_type_RELU;
  static constexpr af_type SIGMOID =
    nn_config_af_type_SIGMOID;
  static constexpr af_type TANH =
    nn_config_af_type_TANH;
  static inline bool af_type_IsValid(int value) {
    return nn_config_af_type_IsValid(value);
  }
  static constexpr af_type af_type_MIN =
    nn_config_af_type_af_type_MIN;
  static constexpr af_type af_type_MAX =
    nn_config_af_type_af_type_MAX;
  static constexpr int af_type_ARRAYSIZE =
    nn_config_af_type_af_type_ARRAYSIZE;
  static inline const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor*
  af_type_descriptor() {
    return nn_config_af_type_descriptor();
  }
  template<typename T>
  static inline const std::string& af_type_Name(T enum_t_value) {
    static_assert(::std::is_same<T, af_type>::value ||
      ::std::is_integral<T>::value,
      "Incorrect type passed to function af_type_Name.");
    return nn_config_af_type_Name(enum_t_value);
  }
  static inline bool af_type_Parse(const std::string& name,
      af_type* value) {
    return nn_config_af_type_Parse(name, value);
  }

  // accessors -------------------------------------------------------

  enum : int {
    kNnArchFieldNumber = 2,
    kAfConfigFieldNumber = 3,
    kNameFieldNumber = 1,
  };
  // repeated uint32 nn_arch = 2;
  int nn_arch_size() const;
  private:
  int _internal_nn_arch_size() const;
  public:
  void clear_nn_arch();
  private:
  ::PROTOBUF_NAMESPACE_ID::uint32 _internal_nn_arch(int index) const;
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >&
      _internal_nn_arch() const;
  void _internal_add_nn_arch(::PROTOBUF_NAMESPACE_ID::uint32 value);
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >*
      _internal_mutable_nn_arch();
  public:
  ::PROTOBUF_NAMESPACE_ID::uint32 nn_arch(int index) const;
  void set_nn_arch(int index, ::PROTOBUF_NAMESPACE_ID::uint32 value);
  void add_nn_arch(::PROTOBUF_NAMESPACE_ID::uint32 value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >&
      nn_arch() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >*
      mutable_nn_arch();

  // repeated .ddrl.nn_config.af_type af_config = 3;
  int af_config_size() const;
  private:
  int _internal_af_config_size() const;
  public:
  void clear_af_config();
  private:
  ::ddrl::nn_config_af_type _internal_af_config(int index) const;
  void _internal_add_af_config(::ddrl::nn_config_af_type value);
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* _internal_mutable_af_config();
  public:
  ::ddrl::nn_config_af_type af_config(int index) const;
  void set_af_config(int index, ::ddrl::nn_config_af_type value);
  void add_af_config(::ddrl::nn_config_af_type value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>& af_config() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* mutable_af_config();

  // string name = 1;
  void clear_name();
  const std::string& name() const;
  void set_name(const std::string& value);
  void set_name(std::string&& value);
  void set_name(const char* value);
  void set_name(const char* value, size_t size);
  std::string* mutable_name();
  std::string* release_name();
  void set_allocated_name(std::string* name);
  GOOGLE_PROTOBUF_RUNTIME_DEPRECATED("The unsafe_arena_ accessors for"
  "    string fields are deprecated and will be removed in a"
  "    future release.")
  std::string* unsafe_arena_release_name();
  GOOGLE_PROTOBUF_RUNTIME_DEPRECATED("The unsafe_arena_ accessors for"
  "    string fields are deprecated and will be removed in a"
  "    future release.")
  void unsafe_arena_set_allocated_name(
      std::string* name);
  private:
  const std::string& _internal_name() const;
  void _internal_set_name(const std::string& value);
  std::string* _internal_mutable_name();
  public:

  // @@protoc_insertion_point(class_scope:ddrl.nn_config)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 > nn_arch_;
  mutable std::atomic<int> _nn_arch_cached_byte_size_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int> af_config_;
  mutable std::atomic<int> _af_config_cached_byte_size_;
  ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_nn_5fconfig_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// nn_config

// string name = 1;
inline void nn_config::clear_name() {
  name_.ClearToEmpty(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArena());
}
inline const std::string& nn_config::name() const {
  // @@protoc_insertion_point(field_get:ddrl.nn_config.name)
  return _internal_name();
}
inline void nn_config::set_name(const std::string& value) {
  _internal_set_name(value);
  // @@protoc_insertion_point(field_set:ddrl.nn_config.name)
}
inline std::string* nn_config::mutable_name() {
  // @@protoc_insertion_point(field_mutable:ddrl.nn_config.name)
  return _internal_mutable_name();
}
inline const std::string& nn_config::_internal_name() const {
  return name_.Get();
}
inline void nn_config::_internal_set_name(const std::string& value) {
  
  name_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), value, GetArena());
}
inline void nn_config::set_name(std::string&& value) {
  
  name_.Set(
    &::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::move(value), GetArena());
  // @@protoc_insertion_point(field_set_rvalue:ddrl.nn_config.name)
}
inline void nn_config::set_name(const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  
  name_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::string(value),
              GetArena());
  // @@protoc_insertion_point(field_set_char:ddrl.nn_config.name)
}
inline void nn_config::set_name(const char* value,
    size_t size) {
  
  name_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), ::std::string(
      reinterpret_cast<const char*>(value), size), GetArena());
  // @@protoc_insertion_point(field_set_pointer:ddrl.nn_config.name)
}
inline std::string* nn_config::_internal_mutable_name() {
  
  return name_.Mutable(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArena());
}
inline std::string* nn_config::release_name() {
  // @@protoc_insertion_point(field_release:ddrl.nn_config.name)
  return name_.Release(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArena());
}
inline void nn_config::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  name_.SetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), name,
      GetArena());
  // @@protoc_insertion_point(field_set_allocated:ddrl.nn_config.name)
}
inline std::string* nn_config::unsafe_arena_release_name() {
  // @@protoc_insertion_point(field_unsafe_arena_release:ddrl.nn_config.name)
  GOOGLE_DCHECK(GetArena() != nullptr);
  
  return name_.UnsafeArenaRelease(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(),
      GetArena());
}
inline void nn_config::unsafe_arena_set_allocated_name(
    std::string* name) {
  GOOGLE_DCHECK(GetArena() != nullptr);
  if (name != nullptr) {
    
  } else {
    
  }
  name_.UnsafeArenaSetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(),
      name, GetArena());
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:ddrl.nn_config.name)
}

// repeated uint32 nn_arch = 2;
inline int nn_config::_internal_nn_arch_size() const {
  return nn_arch_.size();
}
inline int nn_config::nn_arch_size() const {
  return _internal_nn_arch_size();
}
inline void nn_config::clear_nn_arch() {
  nn_arch_.Clear();
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 nn_config::_internal_nn_arch(int index) const {
  return nn_arch_.Get(index);
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 nn_config::nn_arch(int index) const {
  // @@protoc_insertion_point(field_get:ddrl.nn_config.nn_arch)
  return _internal_nn_arch(index);
}
inline void nn_config::set_nn_arch(int index, ::PROTOBUF_NAMESPACE_ID::uint32 value) {
  nn_arch_.Set(index, value);
  // @@protoc_insertion_point(field_set:ddrl.nn_config.nn_arch)
}
inline void nn_config::_internal_add_nn_arch(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  nn_arch_.Add(value);
}
inline void nn_config::add_nn_arch(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  _internal_add_nn_arch(value);
  // @@protoc_insertion_point(field_add:ddrl.nn_config.nn_arch)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >&
nn_config::_internal_nn_arch() const {
  return nn_arch_;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >&
nn_config::nn_arch() const {
  // @@protoc_insertion_point(field_list:ddrl.nn_config.nn_arch)
  return _internal_nn_arch();
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >*
nn_config::_internal_mutable_nn_arch() {
  return &nn_arch_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< ::PROTOBUF_NAMESPACE_ID::uint32 >*
nn_config::mutable_nn_arch() {
  // @@protoc_insertion_point(field_mutable_list:ddrl.nn_config.nn_arch)
  return _internal_mutable_nn_arch();
}

// repeated .ddrl.nn_config.af_type af_config = 3;
inline int nn_config::_internal_af_config_size() const {
  return af_config_.size();
}
inline int nn_config::af_config_size() const {
  return _internal_af_config_size();
}
inline void nn_config::clear_af_config() {
  af_config_.Clear();
}
inline ::ddrl::nn_config_af_type nn_config::_internal_af_config(int index) const {
  return static_cast< ::ddrl::nn_config_af_type >(af_config_.Get(index));
}
inline ::ddrl::nn_config_af_type nn_config::af_config(int index) const {
  // @@protoc_insertion_point(field_get:ddrl.nn_config.af_config)
  return _internal_af_config(index);
}
inline void nn_config::set_af_config(int index, ::ddrl::nn_config_af_type value) {
  af_config_.Set(index, value);
  // @@protoc_insertion_point(field_set:ddrl.nn_config.af_config)
}
inline void nn_config::_internal_add_af_config(::ddrl::nn_config_af_type value) {
  af_config_.Add(value);
}
inline void nn_config::add_af_config(::ddrl::nn_config_af_type value) {
  // @@protoc_insertion_point(field_add:ddrl.nn_config.af_config)
  _internal_add_af_config(value);
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>&
nn_config::af_config() const {
  // @@protoc_insertion_point(field_list:ddrl.nn_config.af_config)
  return af_config_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
nn_config::_internal_mutable_af_config() {
  return &af_config_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
nn_config::mutable_af_config() {
  // @@protoc_insertion_point(field_mutable_list:ddrl.nn_config.af_config)
  return _internal_mutable_af_config();
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace ddrl

PROTOBUF_NAMESPACE_OPEN

template <> struct is_proto_enum< ::ddrl::nn_config_af_type> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::ddrl::nn_config_af_type>() {
  return ::ddrl::nn_config_af_type_descriptor();
}

PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_nn_5fconfig_2eproto
