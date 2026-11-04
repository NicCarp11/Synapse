# SLICC back end

The back end that writes the SLICC state machines is by Nicolai Oswald and Theo Olausson, The
University of Edinburgh. It lives on the `slicc` branch of HeteroGen:
https://github.com/Errare-humanum-est/HeteroGen/tree/slicc

`synapse.py generate` and `synapse.py verify` use it. To install it, from the root of this
repository:

```bash
git clone --depth 1 -b slicc https://github.com/Errare-humanum-est/HeteroGen ../HeteroGen
cp -r ../HeteroGen/Backend/SLICC/. Backend/SLICC/
```

If you use it, please cite HeteroGen (Credits in the main README).
