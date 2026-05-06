<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('/screenshots', [App\Http\Controllers\ScreenshotController::class, 'store']);

Route::post('/screenshots/{id}/update_screenshot', [App\Http\Controllers\ScreenshotController::class, 'update_screenshot']); 

Route::get('/screenshots', [App\Http\Controllers\ScreenshotController::class, 'all_screenshots']);