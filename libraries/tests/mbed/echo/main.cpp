#include "mbed.h"
#include "test_env.h"

#if defined(TARGET_NUCLEO_F103RB) || \
    defined(TARGET_NUCLEO_L152RE) || \
    defined(TARGET_NUCLEO_F302R8) || \
    defined(TARGET_NUCLEO_F030R8) || \
    defined(TARGET_NUCLEO_F401RE) || \
    defined(TARGET_NUCLEO_F411RE) || \
    defined(TARGET_NUCLEO_F072RB) || \
    defined(TARGET_NUCLEO_F334R8) || \
    defined(TARGET_NUCLEO_L053R8)
#define TXPIN     STDIO_UART_TX
#define RXPIN     STDIO_UART_RX
#else
#define TXPIN     USBTX
#define RXPIN     USBRX
#endif

int main() {
    char buf[256];

    Serial pc(TXPIN, RXPIN);
    pc.baud(115200);

    pc.puts("{{");
    pc.puts(TEST_ENV_START);    // Host test is expecting preamble
    pc.puts("}}");

    while (1) {
        pc.gets(buf, 256);
        pc.printf("%s", buf);
    }
}
