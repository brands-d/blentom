blentom.zip: __init__.py LICENSE README.rst src/
	zip -r $@ blentom __init__.py LICENSE README.rst src/

.PHONY: bundle

bundle: blentom.zip