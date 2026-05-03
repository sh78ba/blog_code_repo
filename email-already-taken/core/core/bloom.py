from pybloom_live import BloomFilter

# capacity = expected users, error_rate = false positive rate
email_bloom = BloomFilter(capacity=100000, error_rate=0.001)