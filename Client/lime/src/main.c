/*
 * LiME - Linux Memory Extractor
 * Copyright (c) 2011-2014 Joe Sylve - 504ENSICS Labs
 *
 *
 * Author:
 * Joe Sylve       - joe.sylve@gmail.com, @jtsylve
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details. 
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
 */

#include "lime.h"

// This file
static int write_lime_header(struct resource *);
static int write_padding(size_t);
static int write_range(struct resource *);
static int write_vaddr(void *, size_t);
static int setup(void);
static void cleanup(void);
static int init(void);

// External
extern int write_vaddr_tcp(void *, size_t);
extern int setup_tcp(void);
extern void cleanup_tcp(void);

extern int write_vaddr_disk(void *, size_t);
extern int setup_disk(void);
extern void cleanup_disk(void);

static char * format = 0;
static int mode = 0;
static int method = 0;
static char zero_page[PAGE_SIZE];

char * path = 0;
int dio = 0;
int port = 0;

extern struct resource iomem_resource;

module_param(path, charp, S_IRUGO);
module_param(dio, int, S_IRUGO);
module_param(format, charp, S_IRUGO);

int init_module (void)
{
	if(!path) {
		DBG("No path parameter specified");
		return -EINVAL;
	}

	if(!format) {
		DBG("No format parameter specified");
		return -EINVAL;
	}
	
	DBG("Parameters");
	DBG("  PATH: %s", path);
	DBG("  DIO: %u", dio);
	DBG("  FORMAT: %s", format);

	memset(zero_page, 0, sizeof(zero_page));

	if (!strcmp(format, "raw")) mode = LIME_MODE_RAW;
	else if (!strcmp(format, "lime")) mode = LIME_MODE_LIME;
	else if (!strcmp(format, "padded")) mode = LIME_MODE_PADDED;
	else {
		DBG("Invalid format parameter specified.");
		return -EINVAL;
	}

	method = (sscanf(path, "tcp:%d", &port) == 1) ? LIME_METHOD_TCP : LIME_METHOD_DISK;
	return init();
}

static int init() {
	struct resource *p;
	int err = 0;
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,18)
	resource_size_t p_last = -1;
#else
	__PTRDIFF_TYPE__ p_last = -1;
#endif

	DBG("Initilizing Dump...");

	if((err = setup())) {
		DBG("Setup Error");
		cleanup();
		return err;
	}

	for (p = iomem_resource.child; p ; p = p->sibling) {
		if (strcmp(p->name, LIME_RAMSTR))
			continue;

		if (mode == LIME_MODE_LIME && (err = write_lime_header(p))) {
			DBG("Error writing header 0x%lx - 0x%lx", (long) p->start, (long) p->end);
			break;
		} else if (mode == LIME_MODE_PADDED && (err = write_padding((size_t) ((p->start - 1) - p_last)))) {
			DBG("Error writing padding 0x%lx - 0x%lx", (long) p_last, (long) p->start - 1);
			break;
		}

		if ((err = write_range(p))) {
			DBG("Error writing range 0x%lx - 0x%lx", (long) p->start, (long) p->end);
			break;
		}

		p_last = p->end;
	}
	

	cleanup();

	return err;
}

static int write_lime_header(struct resource * res) {
	long s;

	lime_mem_range_header header;

	memset(&header, 0, sizeof(lime_mem_range_header));
	header.magic = LIME_MAGIC;
	header.version = 1;
	header.s_addr = res->start;
	header.e_addr = res->end;
	
	s = write_vaddr(&header, sizeof(lime_mem_range_header));
	
	if (s != sizeof(lime_mem_range_header)) {
		DBG("Error sending header %ld", s);
		return (int) s;
	}				

	return 0;
}

static int write_padding(size_t s) {
	size_t i = 0;
	int r;

	while(s -= i) {

		i = min((size_t) PAGE_SIZE, s);
		r = write_vaddr(zero_page, i);

		if (r != i) {
			DBG("Error sending zero page: %d", r);
			return r;
		}
	}

	return 0;
}

static int write_range(struct resource * res) {
#if LINUX_VERSION_CODE >= KERNEL_VERSION(2,6,18)
	resource_size_t i, is;
#else
	__PTRDIFF_TYPE__ i, is;
#endif
	struct page * p;
	void * v;
	
	int s;

	for (i = res->start; i <= res->end; i += is) {

		p = pfn_to_page((i) >> PAGE_SHIFT);
        
        is = min((size_t) PAGE_SIZE, (size_t) (res->end - i + 1));

        if (is < PAGE_SIZE) {
        	// We can't map partial pages and 
        	// the linux kernel doesn't use them anyway
        	DBG("Padding partial page: vaddr %p size: %lu", (void *) i, is);
        	write_padding(is);
        } else {
			v = kmap(p);
			s = write_vaddr(v, is);
			kunmap(p);

			if (s != is) {
				DBG("Error writing page: vaddr %p ret: %d", v, s);
				return (int) s;
			}
		}
	}

	return 0;
}

static int write_vaddr(void * v, size_t is) {
	return (method == LIME_METHOD_TCP) ? write_vaddr_tcp(v, is) : write_vaddr_disk(v, is);
}

static int setup(void) {
	return (method == LIME_METHOD_TCP) ? setup_tcp() : setup_disk();
}

static void cleanup(void) {
	return (method == LIME_METHOD_TCP) ? cleanup_tcp() : cleanup_disk();
}

void cleanup_module(void)
{
	
}

MODULE_LICENSE("GPL");
