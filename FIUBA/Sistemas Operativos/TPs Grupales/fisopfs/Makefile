CC = gcc
CFLAGS := -ggdb3 -O2 -Wall -std=c11
CFLAGS += -Wno-unused-function -Wvla -D_FILE_OFFSET_BITS=64


FUSE_CFLAGS := $(shell pkg-config fuse --cflags 2>/dev/null || pkg-config fuse3 --cflags)
FUSE_LIBS   := $(shell pkg-config fuse --libs   2>/dev/null || pkg-config fuse3 --libs)

CFLAGS += $(FUSE_CFLAGS)
LDLIBS += $(FUSE_LIBS)


FS_NAME := fisopfs

SRCS := fisopfs.c fs.c
OBJS := $(SRCS:.c=.o)

all: $(FS_NAME)

$(FS_NAME): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDLIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

format: .clang-files .clang-format
	xargs -r clang-format -i <$<

build:
	./dock build

run:
	./dock run

exec:
	./dock exec

test:
	bash test.sh

clean:
	rm -rf *.o core vgcore.* $(FS_NAME)

.PHONY: all build clean format run exec
