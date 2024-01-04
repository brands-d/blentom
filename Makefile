zip:
	@cd .. && zip -r blentom/blentom.zip blentom -x "*.gitignore*" -x "*__pycache__*" -x "*blender*" -x "*.git*" -x "*.vscode*" -x "*demo*" -x "*.DS_Store*" -x "*Makefile*"
