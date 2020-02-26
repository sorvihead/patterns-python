import click
import unittest


@click.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('TDD')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    test()
