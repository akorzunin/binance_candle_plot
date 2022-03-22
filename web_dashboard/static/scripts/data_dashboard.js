var str = 'pepe';
var style = ['padding: 1rem;',
    'background: linear-gradient( gold, orangered);',
    'text-shadow: 0 2px orangered;',
    'font: 1.3rem/3 Georgia;',
    'color: white;'].join('');

console.log('%c%s', style, str);