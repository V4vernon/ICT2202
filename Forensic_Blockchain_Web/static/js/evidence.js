$(document).ready(() => {
    $.get('/admin/evidence/all',
        function(data){
            var result =  JSON.parse(data);
            var all_div = document.getElementById("all");
            while (all_div.firstChild) {
                all_div.removeChild(all_div.lastChild);
            }
            for( var i = 0; i < result.length; i++) {
                var div = document.createElement('div');
                div.className = "row";
                div.classList.add("mystyle");
                for(var j = 0; j < 7; j++){
                    var childDiv = document.createElement('div');
                    childDiv.className = "col";
                    childDiv.classList.add("mystyle");
                    if (i == result.length - 1) {
                        childDiv.style.borderBottom = "1px solid lightgray"
                    }
                    childDiv.textContent = result[i][j];
                    div.appendChild(childDiv);
                }
                all_div.appendChild(div);
            }
        }
    )
});

setInterval(() => {
    $.get('/admin/evidence/all',
        function(data){
            var result =  JSON.parse(data);
            var all_div = document.getElementById("all");
            while (all_div.firstChild) {
                all_div.removeChild(all_div.lastChild);
            }
            for( var i = 0; i < result.length; i++) {
                var div = document.createElement('div');
                div.className = "row";
                div.classList.add("mystyle");
                for(var j = 0; j < 7; j++){
                    var childDiv = document.createElement('div');
                    childDiv.className = "col";
                    childDiv.classList.add("mystyle");
                    if (i == result.length - 1) {
                        childDiv.style.borderBottom = "1px solid lightgray"
                    }
                    childDiv.textContent = result[i][j];
                    div.appendChild(childDiv);
                }
                all_div.appendChild(div);
            }
        }
    )
}, 60000)
