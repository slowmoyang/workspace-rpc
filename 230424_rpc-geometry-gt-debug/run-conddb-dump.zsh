#!/usr/bin/env zsh
DATA_DIR=./data/

TAG_ARRAY=(
    RecoIdealGeometry_RPC_v2_hlt
    RecoIdealGeometry_RPC_v3_hlt
)

for TAG in ${TAG_ARRAY[@]}; do
    echo ${TAG}
    conddb --db ${DATA_DIR}/${TAG}.db dump ${TAG} > ${DATA_DIR}/${TAG}.xml
done


# https://cms-conddb.cern.ch/cmsDbBrowser/list/Prod/TAGs/RecoIdealGeometry_RPC_v3_hlt
PAYLOAD_ARRAY=(
    accd477271bd4aeeae63444d03fe5fa8f54324dc # older
    0429f37b6663d8a4075f1d9a761f79cb7c73b91d # newer
)

for PAYLOAD in ${PAYLOAD_ARRAY[@]}; do
    echo ${PAYLOAD}
    conddb --db ${DATA_DIR}/RecoIdealGeometry_RPC_v3_hlt.db dump ${PAYLOAD} \
        > ${DATA_DIR}/payload-${PAYLOAD}.xml
done
