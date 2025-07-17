# macOS Permission Setup Guide

## The "Gray Screen" Issue

When you see a gray screen during area selection, it's because macOS is blocking the application from accessing screen recording capabilities.

## Fix Steps:

### 1. Grant Screen Recording Permission
1. Open **System Preferences** (or System Settings on newer macOS)
2. Go to **Security & Privacy** → **Privacy** tab
3. Find **Screen Recording** in the left sidebar
4. Click the lock icon to make changes (enter your password)
5. Look for your Python executable in the list:
   - It might appear as "Python" or "python3"
   - Or as "Terminal" if you're running from terminal
6. Check the box next to it to enable
7. **Important**: Restart the application after granting permission

### 2. Alternative: If You Can't Find Python in the List
1. Click the "+" button to add an application
2. Navigate to your Python installation:
   - For system Python: `/usr/bin/python3`
   - For Homebrew Python: `/opt/homebrew/bin/python3`
   - For conda: `/opt/miniconda3/envs/book-scanner/bin/python`
3. Add it to the allowed applications

### 3. Grant Accessibility Permission (Also Recommended)
1. In the same **Security & Privacy** → **Privacy** section
2. Find **Accessibility** in the left sidebar
3. Add Python there as well (same process as above)

### 4. Restart Required
After granting permissions, you must restart the Python application for changes to take effect.

## Testing Permissions

Run the permission test script to verify everything works:
```bash
conda run -n book-scanner python permission_test.py
```

## Alternative Selection Method

If you're still having issues, I can create an alternative selection method that:
1. Takes a screenshot first
2. Shows it in a window where you can select the area
3. Doesn't require real-time overlay permissions

This method is more reliable on macOS but slightly less convenient.

## Troubleshooting

- **Still seeing gray screen**: Make sure you restarted the app after granting permissions
- **Permission dialog doesn't appear**: Try running the app from Terminal vs. Finder
- **Can't find Python in the list**: Use the "+" button to manually add your Python executable
