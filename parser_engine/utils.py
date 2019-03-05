import collections
import six


def is_sequence(seq):
    """Returns a true if its input is a collections.Sequence (except strings).
    Args:
      seq: an input sequence.
    Returns:
      True if the sequence is a not a string and is a collections.Sequence.
    """
    return (isinstance(seq, collections.Sequence)
            and not isinstance(seq, six.string_types))


def is_string_like(s):
    return isinstance(s, six.string_types) or isinstance(s, six.binary_type) or isinstance(s, bytearray)
