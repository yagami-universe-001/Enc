import asyncio
import json
import os
import subprocess


async def get_media_info(file_path):
    """
    Get media info from a file using ffprobe.
    """
    try:
        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:stream=width,height,codec_name,codec_type,r_frame_rate",
            "-of",
            "json",
            file_path,
        ]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return json.loads(stdout)
        else:
            return None
    except Exception:
        return None


async def extract_thumbnail(input_file, output_file):
    """
    Extract a thumbnail from a video file.
    """
    try:
        command = [
            "ffmpeg",
            "-i",
            input_file,
            "-ss",
            "00:00:01.000",
            "-vframes",
            "1",
            output_file,
        ]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        if process.returncode == 0 and os.path.exists(output_file):
            return output_file
        else:
            return None
    except Exception:
        return None


async def get_video_streams(file_path):
    """
    Get video streams from a file.
    """
    media_info = await get_media_info(file_path)
    if media_info and "streams" in media_info:
        return [s for s in media_info["streams"] if s.get("codec_type") == "video"]
    return []


async def get_subtitle_streams(file_path):
    """
    Get subtitle streams from a file.
    """
    media_info = await get_media_info(file_path)
    if media_info and "streams" in media_info:
        return [s for s in media_info["streams"] if s.get("codec_type") == "subtitle"]
    return []


async def extract_subtitles(input_file, stream_index, output_file):
    """
    Extract subtitles from a video file.
    """
    try:
        command = [
            "ffmpeg",
            "-i",
            input_file,
            "-map",
            f"0:{stream_index}",
            "-c",
            "copy",
            output_file,
        ]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        if process.returncode == 0 and os.path.exists(output_file):
            return output_file
        else:
            return None
    except Exception:
        return None
