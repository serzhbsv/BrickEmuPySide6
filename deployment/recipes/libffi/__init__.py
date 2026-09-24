from pythonforandroid.recipe import Recipe
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory
import sh
import os


class LibffiRecipe(Recipe):
    version = '8fa8837'
    url = 'https://github.com/libffi/libffi/archive/{version}.tar.gz'
    depends = []

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            # Фикс: LT_SYS_SYMBOL_USCORE не находится autoreconf на Ubuntu 24.04
            configure_ac = 'configure.ac'
            if os.path.exists(configure_ac):
                with open(configure_ac, 'r') as f:
                    content = f.read()
                if 'm4_pattern_allow' not in content:
                    with open(configure_ac, 'w') as f:
                        f.write(
                            'm4_pattern_allow([LT_SYS_SYMBOL_USCORE])\n'
                            'm4_pattern_allow([AC_PROG_LD])\n'
                            + content
                        )
                    print('[LIBFFI] Patched configure.ac with m4_pattern_allow')

            shprint(sh.Command('./autogen.sh'), _env=env)
            shprint(
                sh.Command('./configure'),
                '--host=' + arch.command_prefix,
                '--prefix=' + self.get_build_dir(arch.arch),
                '--disable-builddir',
                '--disable-shared',
                '--enable-static',
                _env=env,
            )
            shprint(sh.Make(''), _env=env)


recipe = LibffiRecipe()
