import unittest

from directory import create_directory, list_people


class DirectoryTests(unittest.TestCase):
    def test_lists_synthetic_people_in_order(self):
        connection = create_directory()
        try:
            self.assertEqual(
                list_people(connection),
                [
                    (1, "Ada", "Engineering"),
                    (2, "Grace", "Research"),
                    (3, "Linus", "Operations"),
                ],
            )
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
