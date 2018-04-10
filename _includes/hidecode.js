
<script>
document.addEventListener("DOMContentLoaded", function(e) {
    var cells = document.querySelectorAll('article .cell');
    for(var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        {% if page.hide_code %}
        var curClasses = cell.getAttribute('class');
        cell.setAttribute('class', curClasses + ' hidden');
        {% endif %}
        cell.addEventListener('click', function() {

            var curClasses = this.getAttribute('class');
            if(curClasses.indexOf(' hide_code') !== -1) {
                this.setAttribute('class', curClasses.substring(0, curClasses.length - 10));
            } else {
                this.setAttribute('class', curClasses + ' hide_code');
            }
        });
    }
});
</script>
