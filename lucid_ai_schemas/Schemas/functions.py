# from typing import Type


# def class_mapper(class_: Type[_O], configure: bool = True) -> Mapper[_O]:
#     """Given a class, return the primary :class:`_orm.Mapper` associated
#     with the key.

#     Raises :exc:`.UnmappedClassError` if no mapping is configured
#     on the given class, or :exc:`.ArgumentError` if a non-class
#     object is passed.

#     Equivalent functionality is available via the :func:`_sa.inspect`
#     function as::

#         inspect(some_mapped_class)

#     Using the inspection system will raise
#     :class:`sqlalchemy.exc.NoInspectionAvailable` if the class is not mapped.

#     """
#     mapper = _inspect_mapped_class(class_, configure=configure)
#     if mapper is None:
#         if not isinstance(class_, type):
#             raise sa_exc.ArgumentError(
#                 "Class object expected, got '%r'." % (class_,)
#             )
#         raise exc.UnmappedClassError(class_)
#     else:
#         return mapper
