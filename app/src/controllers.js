const config = require('./../config')

function hello() { 
    return  { 
        msg: 'Hello, first pipeline build 14!', 
        environment: config.ENV_NAME
    }
};

module.exports = {
    hello: hello
}
