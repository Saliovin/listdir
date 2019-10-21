from listdir import listdir
import hashlib
import os


def test_zip_output():
    listdir.zip_output("[101819-1703]list.txt", False)

    hash1 = get_hash("true_copy.zip")
    hash2 = get_hash("[101819-1703]list.txt.zip")

    os.remove("[101819-1703]list.txt.zip")

    assert hash1 == hash2


def test_get_hash():
    with open("hash_test", "w+") as file:
        pass

    assert listdir.get_hash("hash_test") == \
           ("d41d8cd98f00b204e9800998ecf8427e", "da39a3ee5e6b4b0d3255bfef95601890afd80709")

    os.remove("hash_test")


def test_output_row():
    assert listdir.output_row(".", "true_copy.zip", "./true_copy.zip")[1:5] == \
           ("true_copy.zip", 723, "1d6f738239ec7bd4536ec34a570a3f31", "057e26f66e5576a5539f151f3a4ec4692ac3110b")


def get_hash(file):
    block_size = 65536
    md5_hasher = hashlib.md5()
    sha1_hasher = hashlib.sha1()

    with open(file, 'rb') as f:
        block = f.read(block_size)
        while len(block) > 0:
            md5_hasher.update(block)
            sha1_hasher.update(block)
            block = f.read(block_size)

    return md5_hasher.hexdigest(), sha1_hasher.hexdigest()