from telegram import InlineKeyboardButton
from spreadsheet import TYPE_HOLIDAY, TYPE_ILLNESS

hoursKeyboard = [[InlineKeyboardButton('0', callback_data='h:0')],
        [InlineKeyboardButton('1', callback_data='h:1'),
        InlineKeyboardButton('2', callback_data='h:2'),
        InlineKeyboardButton('3', callback_data='h:3'),
        InlineKeyboardButton('4', callback_data='h:4')],

        [InlineKeyboardButton('5', callback_data='h:5'),
        InlineKeyboardButton('6', callback_data='h:6'),
        InlineKeyboardButton('7', callback_data='h:7'),
        InlineKeyboardButton('8', callback_data='h:8')],
        [InlineKeyboardButton('Non compilare questo giorno', callback_data='d:1')]]


minutesKeyboard = [[InlineKeyboardButton('00', callback_data='m:00'),
        InlineKeyboardButton('15', callback_data='m:15'),
        InlineKeyboardButton('30', callback_data='m:30'),
        InlineKeyboardButton('45', callback_data='m:45')]]

ferieKeyboard = [[InlineKeyboardButton('Ferie', callback_data=('t:%d' % TYPE_HOLIDAY)),
        InlineKeyboardButton('Malattia', callback_data=('t:%d' % TYPE_ILLNESS))]]

dayKeyboard = [
        [InlineKeyboardButton('1', callback_data='e:1'),
        InlineKeyboardButton('2', callback_data='e:2'),
        InlineKeyboardButton('3', callback_data='e:3'),
        InlineKeyboardButton('4', callback_data='e:4')],
        [InlineKeyboardButton('5', callback_data='e:5'),
        InlineKeyboardButton('6', callback_data='e:6'),
        InlineKeyboardButton('7', callback_data='e:7'),
        InlineKeyboardButton('8', callback_data='e:8')],
        [InlineKeyboardButton('9', callback_data='e:9'),
        InlineKeyboardButton('10', callback_data='e:10'),
        InlineKeyboardButton('11', callback_data='e:11'),
        InlineKeyboardButton('12', callback_data='e:12')],
        [InlineKeyboardButton('13', callback_data='e:13'),
        InlineKeyboardButton('14', callback_data='e:14'),
        InlineKeyboardButton('15', callback_data='e:15'),
        InlineKeyboardButton('16', callback_data='e:16')],
        [InlineKeyboardButton('17', callback_data='e:17'),
        InlineKeyboardButton('18', callback_data='e:18'),
        InlineKeyboardButton('19', callback_data='e:19'),
        InlineKeyboardButton('20', callback_data='e:20')],
        [InlineKeyboardButton('21', callback_data='e:21'),
        InlineKeyboardButton('22', callback_data='e:22'),
        InlineKeyboardButton('23', callback_data='e:23'),
        InlineKeyboardButton('24', callback_data='e:24')],
        [InlineKeyboardButton('25', callback_data='e:25'),
        InlineKeyboardButton('26', callback_data='e:26'),
        InlineKeyboardButton('27', callback_data='e:27'),
        InlineKeyboardButton('28', callback_data='e:28')],
        [InlineKeyboardButton('29', callback_data='e:29'),
        InlineKeyboardButton('30', callback_data='e:30'),
        InlineKeyboardButton('31', callback_data='e:31')]]