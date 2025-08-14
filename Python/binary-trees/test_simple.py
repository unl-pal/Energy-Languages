
import unittest
from binarytrees import make_tree, check_tree, make_check, get_argchunks

class TestBinaryTreesBasics(unittest.TestCase):
    def test_make_tree_shapes(self):
        # depth 0 -> (None, None)
        t0 = make_tree(0)
        self.assertEqual(t0, (None, None))

        # depth 1 -> ((None,None),(None,None))
        t1 = make_tree(1)
        self.assertEqual(t1, ((None, None), (None, None)))

    def test_check_tree_counts_total_nodes(self):
        # total nodes in full binary tree of depth d is 2^(d+1) - 1
        self.assertEqual(check_tree(make_tree(0)), 1)
        self.assertEqual(check_tree(make_tree(1)), 3)
        self.assertEqual(check_tree(make_tree(2)), 7)
        self.assertEqual(check_tree(make_tree(3)), 15)

    def test_make_check_matches_check_tree(self):
        for d in range(0, 5):
            self.assertEqual(make_check((0, d)), check_tree(make_tree(d)))

    def test_get_argchunks_structure_and_total(self):
        # i items, chunked by chunksize, each element is a (k, d) pair
        i, d, chunksize = 10, 3, 4
        chunks = list(get_argchunks(i, d, chunksize=chunksize))
        # chunk sizes should be [4,4,2]
        sizes = [len(c) for c in chunks]
        self.assertEqual(sizes, [4, 4, 2])
        # each element should be a (k, d) tuple with correct d
        for chunk in chunks:
            for (k, dd) in chunk:
                self.assertIsInstance(k, int)
                self.assertEqual(dd, d)
        # total elements equals i
        self.assertEqual(sum(sizes), i)

if __name__ == "__main__":
    unittest.main()
