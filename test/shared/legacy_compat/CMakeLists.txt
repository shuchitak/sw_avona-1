
if((${CMAKE_SYSTEM_NAME} STREQUAL XCORE_XS3A) OR (${CMAKE_SYSTEM_NAME} STREQUAL XCORE_XS2A))
    ## Create library target
    add_library(avona_test_deps_legacy_compat INTERFACE)
    target_include_directories(avona_test_deps_legacy_compat
        INTERFACE
            api
    )
    ## Create an alias
    add_library(avona_test_deps::legacy_compat ALIAS avona_test_deps_legacy_compat)
endif()
