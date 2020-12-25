
_check_result()
{
    if [ $? -ne 0 ]; then
        exit 1
    else
        echo "[√] last execution successful."
    fi
}

hexo server > /dev/null 2>&1 &
sleep 20 && curl -Is http://localhost:4000/ | head -n 1
_check_result

hexo clean
_check_result

hexo generate -deploy
_check_result
