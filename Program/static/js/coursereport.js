var reportText = $('#txtReport')

function generateReport() {
    console.log("Sending request");
    $.ajax({
        type: "POST",
        url: "/coursereport",
        success: function (response) {
            console.log("Got response!");
            reportText.html('')
            let reportHeadingHtml = '<br><h1>Balham College</h1>\n<h2 class="text-center">Courses Report</h2><br>'
            reportText.html(reportText.html()+reportHeadingHtml)
            $.each(response["courses"], function (index, value){
                console.log(`Adding course ${index} to report`)
                let reportObjectHtml = `<hr>\n<h3>${value["name"]}</h3>\n` +
                    '            <table class="table table-bordered">\n' +
                    '                <tr>\n' +
                    '                    <th>ID</th>\n' +
                    '                    <th>Credits</th>\n' +
                    '                    <th>Status</th>\n' +
                    '                    <th>Fee</th>\n' +
                    '                    <th>Programme Name</th>\n' +
                    '                </tr>\n' +
                    '                <tr>\n' +
                    `                    <td>${value["id"]}</td>\n` +
                    `                    <td>${value["credits"]}</td>\n` +
                    `                    <td>${value["status"].toUpperCase()}</td>\n` +
                    `                    <td>${value["fee"]}</td>\n` +
                    `                    <td>${value["programme"]}</td>\n` +
                    '                </tr>\n' +
                    '            </table>\n' +
                    '            <table class="table table-bordered">\n' +
                    '                <tr>\n' +
                    '                    <th>Enrolments</th>\n' +
                    '                    <th>Assessments</th>\n' +
                    '                </tr>\n' +
                    '                <tr>\n' +
                    `                    <td>${value["enrolments"]}</td>\n` +
                    `                    <td>${value["assessments"]}</td>\n` +
                    '                </tr>\n' +
                    '            </table><br>'
                reportText.html(reportText.html()+reportObjectHtml)
            })
        }
    });
}

$('#courseReportForm').submit(function (){
   generateReport();
   return false;
});