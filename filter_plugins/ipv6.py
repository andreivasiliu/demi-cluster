class FilterModule(object):
    def filters(self):
        def get_ipv6_suffix(text):
            segments = text.split(':')
            return ':'.join(segments[4:])
        
        return {
            'get_ipv6_suffix': get_ipv6_suffix,
        }
