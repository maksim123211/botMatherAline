from app.bot.assets import Command, Callback

commands, callbacks = ([], [],)


def message(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            commands.append(Command(name=kwargs['name'], handler=handler,
                                    dialog=kwargs['dialog'] if 'dialog' in kwargs else 'default',
                                    admin=(kwargs['admin'] if 'admin' in kwargs else False),
                                    with_args=(kwargs['with_args'] if 'with_args' in kwargs else False)))
        else:
            return False

    return with_args


def callback(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            callbacks.append(Callback(name=kwargs['name'], handler=handler, admin=(kwargs['admin']
                                                                                   if 'admin' in kwargs
                                                                                   else False)))
        else:
            return False

    return with_args
