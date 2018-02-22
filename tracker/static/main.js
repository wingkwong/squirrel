var ExpenseTracker = {};

$(function() {
    if ($('.expense-overview').length) ExpenseTracker.Filter.init();
});

ExpenseTracker.Filter = {
    init: function() {
        var self = this;
        $('.open-filter-btn').click(function(e) {
            e.preventDefault();
            self.openFilterPanel();
        });

        $('.closebtn').click(function(e) {
            e.preventDefault();
            self.closeFilterPanel();
        });
    },
    openFilterPanel: function() {
        document.getElementById("filterPanel").style.width = "100%";
    },
    closeFilterPanel: function() {
        document.getElementById("filterPanel").style.width = "0";
    }
}