## Wi-viz makefile
# Supply your own C cross-compiler; I recommend the one from the OpenWRT buildroot
# Also requires a libpcap to link with, use libpcap.a for static, .so for shared
CC=/opt/toolchain-mipsel_3.3.6_BRCM24/bin/mipsel-linux-uclibc-gcc
LIBS=libpcap.a

CCOPTS=-O2 -Os -pipe -mips32 -mtune=mips32
INCLUDE=/opt/toolchain-mipsel_3.3.6_BRCM24/lib
SOURCES=wiviz.c wl_access.c channelhopper.c
OBJS=wiviz.o wl_access.o channelhopper.o
TARGET=wiviz

wiviz: ${OBJS}
	${CC} ${CCOPTS} -I${INCLUDE} -I. -o ${TARGET} ${OBJS} ${LIBS}

wiviz.o: wiviz.c
	${CC} ${CCOPTS} -I${INCLUDE} -I. -c ${SOURCES}
wl_access.o: wl_access.c
	${CC} ${CCOPTS} -I${INCLUDE} -I. -c ${SOURCES}
channelhopper.o: channelhopper.c
	${CC} ${CCOPTS} -I${INCLUDE} -I. -c ${SOURCES}

remake:
	touch wiviz.c wl_access.c channelhopper.c
