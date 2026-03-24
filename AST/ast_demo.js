const parse = require('@babel/parser').parse
const generator = require('@babel/generator').default;
const traverse = require('@babel/traverse').default;
const types = require('@babel/types')
const fs = require('fs');
const { exit } = require('process');
const {a0_0x1d08,_0x55e02c,_0x5265ff}=require('./decrypt.js')


// 待反混淆的文件
let jsCode = fs.readFileSync('./input.js', { encoding: 'utf-8' })
let ast = parse(jsCode);

//十六进制转十进制
traverse(ast,{
    NumericLiteral:{
        exit:function(path){
            // console.log(path.toString())
            path.replaceWith(types.NumericLiteral(path.node.value))
            path.skip()
        }
    }
})


traverse(ast,{
    CallExpression:{
        exit:function(path){
            if(path.node.callee&&path.node.callee.name=='a0_0x1d08'&&path.node.arguments.length==1){
                // console.log(path.toString())
                path.replaceWith(types.stringLiteral(a0_0x1d08(path.node.arguments[0].value)))
                // console.log(path.toString())
            }


        }
    }
})

traverse(ast,{
    CallExpression:{
        exit:function(path){
            if(['_0x55e02c','_0x5265ff','_0x3ec950','_0x522db3','_0xd1d032'].includes(path.node.callee.name)){
                // console.log(path.toString())


                if(path.node.callee.name=='_0x5265ff'){
                    path.replaceWith(types.stringLiteral(_0x5265ff(path.node.arguments[0].value)))
                }
                else{
                    path.replaceWith(types.stringLiteral(_0x55e02c(path.node.arguments[0].value)))
                }
                // console.log(path.toString())
            }


        }
    }
})


traverse(ast,{
    MemberExpression:{
        exit:function(path){
            // console.log(path.toString())
            if(path.node.object.name&&path.node.object.name=='_0x1acbfd'&&types.isNumericLiteral(path.node.property)){
                let _0x1acbfd=path.scope.getBinding('_0x1acbfd')
                path.replaceWith(_0x1acbfd.path.node.init.elements[path.node.property.value])
                // console.log(path.toString())
            }
            // console.log(path.toString())

        }
    }
})

traverse(ast,{
    MemberExpression:{
        exit:function(path){
            // console.log(path.toString())
            if(path.node.object.name&&path.node.object.name=='_0x447c80'&&types.isNumericLiteral(path.node.property)){
                let _0x1acbfd=path.scope.getBinding('_0x447c80')
                path.replaceWith(_0x1acbfd.path.node.init.elements[path.node.property.value])
                // console.log(path.toString())
            }
            // console.log(path.toString())

        }
    }
})
traverse(ast,{
    MemberExpression:{
        exit:function(path){
            // console.log(path.toString())
            if(path.node.object.name&&path.node.object.name=='_0x1fe63e'&&types.isNumericLiteral(path.node.property)){
                let _0x1acbfd=path.scope.getBinding('_0x1fe63e')
                path.replaceWith(_0x1acbfd.path.node.init.elements[path.node.property.value])
                // console.log(path.toString())
            }
            // console.log(path.toString())

        }
    }
})
// 清除死代码
ast = parse(generator(ast, { compact: true }).code)
traverse(ast, {
    VariableDeclarator: {
        exit(path) {
            let { init, id } = path.node;
            if (!types.isObjectExpression(init) && !types.isIdentifier(id)) return;
            let { scope } = path;
            let binding = scope.getBinding(id.name);
            if (binding.referencePaths.length !== 0) return;//被引用次数
            path.remove();
        }
    }
})


// 语法数转JS代码
let { code } = generator(ast, { compact: false });
// console.log(code);

// 保存
fs.writeFile('./output.js', code, (err) => {
});
