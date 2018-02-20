var ExpenseTracker = {};

$(function() {
    if ($('.expense-overview').length) ExpenseTracker.Filter.init();
    if ($('.expense-analysis').length) ExpenseTracker.Analysis.init();
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

ExpenseTracker.Analysis = {
    init: function() {
        $.ajax({
            method: 'get',
            url: '/api/expense/',
            success: function(data) {
                var data = JSON.parse(data.expense);
                var totalAmount;
                var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                var monthlyExpenseCnt;

                var type = [];
                var randomColorSet = [
                    "#f38b4a", "#56d798", "#ff8397", "#6970d5", '#6666FF',
                    '#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
                    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
                    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
                    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
                    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
                    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
                    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
                    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
                    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
                    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6'
                ];

                // categorize expense type
                for (var i = 0; i < data.length; i++) {
                    if ($.inArray(data[i].fields.type, type) == -1) type.push(data[i].fields.type);
                }

                // group data by type
                var groupByType = [];
                for (var i = 0; i < type.length; i++) {
                    var t = data.filter(function(el) {
                        return el.fields.type == type[i];
                    });
                    groupByType.push(t);
                }

                // calculate the total amount per type
                var totalAmountByType = [];

                for (var i = 0; i < groupByType.length; i++) {
                    monthlyExpenseCnt = new Array(12).fill(0);
                    totalAmount = [];

                    for (var j = 0; j < groupByType[i].length; j++) {
                        monthlyExpenseCnt[new Date(groupByType[i][j].fields.date).getMonth()] += groupByType[i][j].fields.amount;
                    }

                    for (var k = 0; k < monthlyExpenseCnt.length; k++) {
                        var o = {};
                        o.x = months[k];
                        o.y = monthlyExpenseCnt[k];
                        totalAmount.push(o);
                    }

                    totalAmountByType.push(totalAmount);
                }

                // prepare chart dataset
                var dataset = [];
                for (var i = 0; i < type.length; i++) {
                    var color = randomColorSet[Math.floor((Math.random() * randomColorSet.length))];
                    var o = {
                        label: type[i],
                        backgroundColor: color,
                        borderColor: color,
                        data: totalAmountByType[i],
                        fill: false
                    };
                    dataset.push(o);
                }

                // init line chart
                var ctx = document.getElementById("myChart").getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: months,
                        datasets: dataset
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Expense Annual Chart'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Month'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Value'
                                }
                            }]
                        }
                    }
                });
            }
        });

    }
}