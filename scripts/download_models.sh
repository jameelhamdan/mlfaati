#!/bin/bash
echo "Downloading models..."
mkdir -p ./bin/models/
curl -LJ https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/inception_v3_weights_tf_dim_ordering_tf_kernels.h5 --output ./bin/models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5
echo "Finished downloading"
exec "$@"
