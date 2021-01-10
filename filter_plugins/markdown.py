class FilterModule(object):
    def filters(self):
        def markdown(text):
            import mistune

            return mistune.markdown(text)
        
        return {
            'markdown': markdown,
        }
