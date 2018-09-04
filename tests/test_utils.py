import unittest
from vmc.utils.decorators import typecheck


class TestDecorators(unittest.TestCase):

    def test_typecheck(self):
        @typecheck(int, (str, int), name=str, sex=(int, str))
        def foo(*args, **kwargs):
            self.assertIsInstance(args[0], int)
            self.assertIsInstance(args[1], (str, int))
            if 'name' in kwargs:
                self.assertIsInstance(kwargs['name'], str)
            if 'sex' in kwargs:
                self.assertIsInstance(kwargs['sex'], (int, str))

        # # check if number matches
        # with self.assertRaises(ValueError):
        #     # check if keywords number matches
        #     foo(2, 111, sex="male")

        with self.assertRaises(TypeError):
            # check if argument number matches
            foo(2, name="Sam", sex="male")

        # check if type matches
        with self.assertRaises(TypeError):
            # check if argument type matches
            foo("name", 111, name="str", sex="male")

        with self.assertRaises(TypeError):
            # check if keyword type matches
            foo(1, 111, name=2, sex=2)

        # check if multi-type works
        foo(1, "name", name="Peter", sex="male")
        foo(1, "name", name="Peter", sex=2)

        foo(1, 111, name="Peter", sex="male")
        foo(1, 111, name="Peter", sex=2)


if __name__ == '__main__':
    unittest.main()
