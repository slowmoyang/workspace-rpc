#!/user/bin/env zsh
LOG_FILE=./step3.log
python3 dev_step3.py > ${LOG_FILE} 2>&1 &
tail -f ${LOG_FILE}
