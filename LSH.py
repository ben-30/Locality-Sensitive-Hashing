from random import shuffle

# DATA

a = "1170 is a good class."
b = "1170 is a great class."
c = "I wish to take a nap after the project."

print("a:", a)
print("b:", b)
print("c:", c)
print()


# SHINGLING

def shingle(text, k):
    shingle_set = []
    for i in range(len(text) - k + 1):
        shingle_set.append(text[i:i + k])
    return set(shingle_set)


k = 2
a_shingle = shingle(a, k)
b_shingle = shingle(b, k)
c_shingle = shingle(c, k)

print("a_shingle:", a_shingle)
print("b_shingle:", b_shingle)
print("c_shingle:", c_shingle)
print()


# JACCARD INDEX

def jaccard(a: set, b: set):
    return len(a.intersection(b)) / len(a.union(b))


print("Jaccard (a/b):", jaccard(a_shingle, b_shingle))
print("Jaccard (a/c):", jaccard(a_shingle, c_shingle))
print("Jaccard (b/c):", jaccard(b_shingle, c_shingle))
print()


# ONE-HOT ENCODING

combine_shingles = list(a_shingle.union(b_shingle).union(c_shingle))
a_1hot = []
b_1hot = []
c_1hot = []

for shingle in combine_shingles:
    if shingle in a_shingle:
        a_1hot.append(1)
    else:
        a_1hot.append(0)
    if shingle in b_shingle:
        b_1hot.append(1)
    else:
        b_1hot.append(0)
    if shingle in c_shingle:
        c_1hot.append(1)
    else:
        c_1hot.append(0)

print("Combined Shingles:", combine_shingles)
print("a_1hot:", a_1hot)
print("b_1hot:", b_1hot)
print("c_1hot:", c_1hot)
print()


# MIN-HASHING

# create one MinHash function, randomized order of numbers
def create_hash_func(size):
    hash_ex = list(range(1, len(combine_shingles) + 1))
    shuffle(hash_ex)
    return hash_ex


# create MinHash function for each position in signature
def build_minhash_func(combine_size, signature_length):
    hashes = []
    for _ in range(signature_length):
        hashes.append(create_hash_func(combine_size))
    return hashes


# create all MinHash functions
signature_length = 20
minhash_func = build_minhash_func(len(combine_shingles), signature_length)


# create signature for each sparse vector
def create_hash(vector: list):
    global count
    signature = []
    for func in minhash_func:
        if count == 1:
            print("MinHash function for first spot of a_sig:", func)
            print()
            count = 0

        for i in range(1, len(combine_shingles) + 1):
            idx = func.index(i)
            signature_val = vector[idx]
            if signature_val == 1:
                signature.append(idx)
                break
    return signature


count = 1
a_sig = create_hash(a_1hot)
b_sig = create_hash(b_1hot)
c_sig = create_hash(c_1hot)

print("a_sig:", a_sig)
print("b_sig:", b_sig)
print("c_sig:", c_sig)
print()

# JACCARD INDEX COMPARISON

print("Jaccard (a_sig/b_sig):", jaccard(set(a_sig), set(b_sig)))
print("Jaccard (a_sig/c_sig):", jaccard(set(a_sig), set(c_sig)))
print("Jaccard (b_sig/c_sig):", jaccard(set(b_sig), set(c_sig)))
print()


# BANDING

def split_vector(signature, b):
    assert len(signature) % b == 0
    r = int(len(signature) / b)
    subvecs = []
    for i in range(0, len(signature), r):
        subvecs.append(signature[i: i + r])
    return subvecs


band_constant = 10
a_band = split_vector(a_sig, band_constant)
b_band = split_vector(b_sig, band_constant)
c_band = split_vector(c_sig, band_constant)

print("a_band", a_band)
print("b_band", b_band)
print("c_band", c_band)
print()


for a_rows, b_rows in zip(a_band, b_band):
    if a_rows == b_rows:
        print(f"Candidate pair (a_band/b_band): {a_rows} == {b_rows}")
        break

for a_rows, c_rows in zip(a_band, c_band):
    if a_rows == c_rows:
        print(f"Candidate pair (a_band/c_band): {a_rows} == {c_rows}")
        break

for b_rows, c_rows in zip(b_band, c_band):
    if b_rows == c_rows:
        print(f"Candidate pair (b_band/c_band): {b_rows} == {c_rows}")
        break
