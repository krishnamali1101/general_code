import timed

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print '%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000)
        return result
    return timed


# Adding decorator to the method
@timeit
def get_all_employee_details(**kwargs):
    print('employee details')

# The code will look like this after removing the redundant code.

logtime_data ={}
get_all_employee_details(log_time=logtime_data)

# log_time and log_name are optional. Make use of them accordingly when needed.
