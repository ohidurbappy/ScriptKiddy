// You will also need to create a gmail filter to add the 'discord' label
// to any emails you want sent to discord
// must add gmail api from Resource > Advanced Google Services
// add time trigger for this project in google app script homepage (to run periodically)
// to run it -> run -> sendEmailsToDiscord (runs once)

function truncate(str, n) {
    return (str.length > n) ? str.substr(0, n - 1) + '...' : str;
};

function sleepFor(sleepDuration) {
    var now = new Date().getTime();
    while (new Date().getTime() < now + sleepDuration) {
        /* do nothing */
    }
}

async function sendEmailsToDiscord() {
    var label = GmailApp.getUserLabelByName('New');
    var messages = [];
    var threads = label.getThreads();

    for (var i = 0; i < threads.length; i++) {
        messages = messages.concat(threads[i].getMessages())
    }

    for (var i = 0; i < messages.length; i++) {

        var message = messages[i];
        Logger.log(message);
        
        var output = message.getFrom() + ": " + message.getSubject();
        //output += '\n*From:* ' + message.getFrom();
        //output += '\n*to:* ' + message.getTo();
        //output += '\n*cc:* ' + message.getCc();
        //output += '\n*Date:* ' + message.getDate();
        //output += '\n*Subject:* ' + message.getSubject();
        //output += '\n*Body:* ' + message.getPlainBody();
        Logger.log(output);

        var payload = {
            //'username': 'Forum Updates Bot',
            'content': output,
            'embeds': [{
                'title': message.getFrom() + " sent a new Email",
                "url": "https://gmail.com",
                'description': `You have received a new Email on [Gmail](https://www.gmail.com) from ${message.getFrom()} to ${message.getTo} at ${message.getDate()}`,
                "color": 5439368,
                "footer": {
                    "icon_url": "https://cdn.discordapp.com/attachments/740262095827894322/746756267048960020/gmail.png",
                    "text": "Gmail Discord Notifier"
                },
                "fields": [{
                        "name": "From",
                        "value": message.getFrom()
                    },
                    {
                        "name": "To",
                        "value": message.getTo()
                    }, 
                    {
                        "name": "Subject",
                        "value": message.getSubject()
                    },
                    {
                        "name": "Message",
                        "value": truncate(message.getPlainBody(), 1000)
                    }

                ]
            }, ]
        };

        var options = {
            'method': 'post',
            'payload': Utilities.jsonStringify(payload),
            'muteHttpExceptions': true,
            "headers": {
                "Content-Type": "application/json"
            }
        };

        var webhookURL = 'PUT_YOUR_DISCORD_WEBHOOK_URL_HERE';
        UrlFetchApp.fetch(webhookURL, options);
        threads[i].removeLabel(label);

    }

    //   label.removeFromThreads(threads);
}
