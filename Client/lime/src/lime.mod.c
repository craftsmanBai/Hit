#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
 .name = KBUILD_MODNAME,
 .init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
 .exit = cleanup_module,
#endif
 .arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x49ce6154, "module_layout" },
	{ 0xb3bd8450, "sock_setsockopt" },
	{ 0x4c4fef19, "kernel_stack" },
	{ 0x3ec8886f, "param_ops_int" },
	{ 0x69a358a6, "iomem_resource" },
	{ 0xe4f0a7bf, "filp_close" },
	{ 0xc5eebfaa, "sock_create_kern" },
	{ 0x72aa82c6, "param_ops_charp" },
	{ 0x42224298, "sscanf" },
	{ 0x895ddae, "sock_sendmsg" },
	{ 0xa1c76e0a, "_cond_resched" },
	{ 0xb4390f9a, "mcount" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0xf8bf9dc0, "vfs_write" },
	{ 0xe8c78b99, "filp_open" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";


MODULE_INFO(srcversion, "B933A2B28E15C70CDE826BD");
