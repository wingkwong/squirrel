var ExpenseTracker = {};

$(function(){
    if($('.expense-overview').length) ExpenseTracker.Filter.init();
    if($('.expense-analysis').length) ExpenseTracker.Analysis.init();
});

ExpenseTracker.Filter = {
    init: function(){
        var self = this;
        $('.open-filter-btn').click(function(e){
            e.preventDefault();
            self.openFilterPanel();
        });

        $('.closebtn').click(function(e){
            e.preventDefault();
            self.closeFilterPanel();
        });
    },
    openFilterPanel: function(){
        document.getElementById("filterPanel").style.width = "100%";
    },
    closeFilterPanel: function(){
        document.getElementById("filterPanel").style.width = "0";
    }
}

ExpenseTracker.Analysis = {
    init: function(){
        $.ajax({
                method: 'get',
                url : '/api/expense/',
                success: function(data){
                    var data = JSON.parse(data.expense);
                    var chartData = [];
                    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                    var monthlyExpenseCnt = new Array(12).fill(0);

                    for(var i=0; i< data.length; i++){
                        monthlyExpenseCnt[new Date(data[i].fields.date).getMonth()] += data[i].fields.amount;
                    }

                    for(var i=0; i< monthlyExpenseCnt.length; i++){
                        var o = {};
                        o.x = months[i];
                        o.y = monthlyExpenseCnt[i];
                        chartData.push(o);
                    }

                   var ctx = document.getElementById("myChart").getContext('2d');
                   var myChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: months,
                            datasets: [{
                                label: "Total Amount",
                                backgroundColor: "rgb(255, 99, 132)",
                                borderColor: "rgb(255, 99, 132)",
                                data: chartData,
                                fill: false
                            }]
                        },
                        options: {
                            responsive: true,
                            title:{
                                display:true,
                                text:'Expense Annual Chart'
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
