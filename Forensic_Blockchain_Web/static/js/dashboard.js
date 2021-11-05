$(document).ready(() => {
    $.get('/home/latest',
        function(data){
            var result =  JSON.parse(data);
            var latest_div = document.getElementById("magic");
            while (latest_div.firstChild) {
                latest_div.removeChild(latest_div.lastChild);
            }
            for( var i = 0; i < 6; i++) {
                var div = document.createElement('div');
                div.className = "row";
                div.classList.add("mystyle");
                for(var j = 0; j < 6; j++){
                    var childDiv = document.createElement('div');
                    childDiv.className = "col";
                    childDiv.classList.add("mystyle");
                    childDiv.textContent = result[i][j];
                    div.appendChild(childDiv);
                }
                latest_div.appendChild(div);
            }
        }
    )
});

setInterval(() => {
    $.get('/home/latest',
        function(data){
            var result =  JSON.parse(data);
            var latest_div = document.getElementById("magic");
            while (latest_div.firstChild) {
                latest_div.removeChild(latest_div.lastChild);
            }
            for( var i = 0; i < 6; i++) {
                var div = document.createElement('div');
                div.className = "row";
                div.classList.add("mystyle");
                for(var j = 0; j < 6; j++){
                    var childDiv = document.createElement('div');
                    childDiv.className = "col";
                    childDiv.classList.add("mystyle");
                    childDiv.textContent = result[i][j];
                    div.appendChild(childDiv);
                }
                latest_div.appendChild(div);
            }
        }
    )
}, 60000)
