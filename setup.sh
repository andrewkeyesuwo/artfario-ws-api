rm function*.zip
cd lambdaenv/lib/python3.7/site-packages/
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py
