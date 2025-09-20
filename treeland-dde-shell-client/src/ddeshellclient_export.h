#ifndef DDESHELLCLIENT_EXPORT_H
#define DDESHELLCLIENT_EXPORT_H

// Linux-only export macro (GCC/Clang visibility attributes)
#if defined(__GNUC__) || defined(__clang__)
    #if defined(DDESHELLCLIENT_LIBRARY)
        #define DDESHELLCLIENT_EXPORT __attribute__((visibility("default")))
    #else
        #define DDESHELLCLIENT_EXPORT
    #endif
#else
    #define DDESHELLCLIENT_EXPORT
#endif

#endif // DDESHELLCLIENT_EXPORT_H
