#! /bin/bash
while getopts ":m:t:f:k:s:v:e:" opt; do
    case $opt in
        m) SIMILAR=$OPTARG
        ;;
        t) TERM=$OPTARG
        ;;
        f) FOLDER=$OPTARG
        ;;
        k) API_KEY_PATH=$OPTARG
        ;;
        s) API_SERVER=$OPTARG
        ;;
        v) PY_VIRTUAL_ENV=$OPTARG
        ;;
        e) EXT_ROOT=$OPTARG
        ;;
        \?) echo "Invalid option -$OPTARG" >&2
        ;;
    esac
done

cd "$EXT_ROOT/host"

# set virtual env when present
if [ -z "$PY_VIRTUAL_ENV" ]
then
    echo "virtual env is empty"
else
    source $PY_VIRTUAL_ENV
fi

# similarity search
if [ -z "$SIMILAR" ]
then
    echo "similar is empty"
else
    python "$EXT_ROOT/host/zmlp-api.py" -k $API_KEY_PATH -s $API_SERVER -m $SIMILAR
fi

# term search
if [ -z "$TERM" ]
then
    echo "term is empty"
else
    python "$EXT_ROOT/host/zmlp-api.py" -k $API_KEY_PATH -s $API_SERVER -t $TERM
fi

# term search
if [ -z "$FOLDER" ]
then
    echo "term is empty"
else
    python "$EXT_ROOT/host/zmlp-api.py" -k $API_KEY_PATH -s $API_SERVER -f $FOLDER
fi

echo "done running command"
