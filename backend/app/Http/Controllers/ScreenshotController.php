<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Screenshot;
use Illuminate\Support\Facades\Redis;
use App\Events\ScreenshotCompleted;

class ScreenshotController extends Controller
{

    public function store(Request $request)
    {
        $validated = $request->validate(['url' => 'required|url']);

        $screenshot = Screenshot::create([
            'url'    => $validated['url'],
            'status' => 'pending',
            'full_size' => $request->full_size
        ]);

        Redis::publish('screenshot_queue', json_encode([
            'id'  => $screenshot->id,
            'url' => $screenshot->url,
            'full_size' => $screenshot->full_size
        ]));

        return response()->json($screenshot);
    }

    public function update_screenshot(Request $request, $id)
    {
        $screenshot = Screenshot::find($id);
        $screenshot->update([
            'status'=>$request->status,
            'file_path'=> $request->file_path
        ]);
        ScreenshotCompleted::dispatch($screenshot->id, $screenshot->status, $screenshot->file_path, $screenshot->url);
        
        return response()->json($screenshot);
    }

    public function all_screenshots(Request $request)
    {
        $screenshots = Screenshot::all();
        return response()->json($screenshots);
    }
}