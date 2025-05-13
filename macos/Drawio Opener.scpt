on open theFiles
	repeat with fileName in theFiles
		if ((fileName as string) contains ".drawio.") then
			tell application "draw.io"
				try
					open file fileName
				end try
			end tell
		else
			tell application "Preview"
				try
					open file fileName
				end try
			end tell
		end if
	end repeat
end open
