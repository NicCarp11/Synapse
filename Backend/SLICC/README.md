# SLICC back end

The back end that writes the SLICC state machines is by Nicolai Oswald and Theo Olausson, The
University of Edinburgh. It lives on the `slicc` branch of HeteroGen:
https://github.com/Errare-humanum-est/HeteroGen/tree/slicc

`synapse.py generate` and `synapse.py verify` use it. To install it, from the root of this
repository:

```bash
git clone --depth 1 -b slicc https://github.com/Errare-humanum-est/HeteroGen ../HeteroGen
cp -r ../HeteroGen/Backend/SLICC/. Backend/SLICC/
git apply --whitespace=nowarn patches/slicc-backend.patch
```

The patch adds what Synapse needs on top of it: the proxy controller, gem5 v20 support and the entry
point that uses them. If you use the back end, please cite HeteroGen (Credits in the main README).
