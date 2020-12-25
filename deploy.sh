
_check_result()
{
    if [ $? -ne 0 ]; then
        exit 1
    else
        echo "[√] last execution successful."
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
check_server
clean
generate
copy_readme
deploy

exit 0







