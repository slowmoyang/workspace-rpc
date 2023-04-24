#!/usr/bin/env zsh
DATA_DIR=./data/
if [ ! -d ${DATA_DIR} ]; then
    mkdir -vp ${DATA_DIR}
fi

TAG_ARRAY=(
    RecoIdealGeometry_RPC_v2_hlt
    RecoIdealGeometry_RPC_v3_hlt
)

for TAG in ${TAG_ARRAY[@]}; do
    print -- ${TAG}
    conddb_import \
        -f frontier://FrontierProd/CMS_CONDITIONS \
        -t ${TAG} \
        -i ${TAG} \
        -c sqlite_file:${DATA_DIR}/${TAG}.db
done
