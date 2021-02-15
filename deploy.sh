
_check_result()
{
    if [ $? -ne 0 ]; then
        exit 1
    else
        echo "[√] last command was successfully executed."
    fi
}

kill_port_4000_pid()
{
    PIDS=`netstat -ano | findstr :4000 | awk '{print $5}'`
    if [ -z "${PIDS}" ]; then
        echo "[√] ready to go."
    else 
        echo "port 4000 is using by another process."
        for pid in $PIDS
        do
            tskill $pid
        done
        exit 1
    fi
}

check_server()
{
    hexo server > /dev/null 2>&1 &
    sleep 20 && curl -Is http://localhost:4000/ | head -n 1
    _check_result
}

clean()
{
    hexo clean
    _check_result
}

generate()
{
    hexo generate
    _check_result
}

copy_readme()
{
    if [ -d public/ ];then
        rm -rf public/README.*
        cp source/README.md public/
        ls public/README.md
        _check_result
    fi
}

deploy(){
    hexo deploy
    _check_result
}

########################
# Update Blog Websites #
########################
kill_port_4000_pid
check_server
clean
generate
copy_readme
deploy

exit 0







