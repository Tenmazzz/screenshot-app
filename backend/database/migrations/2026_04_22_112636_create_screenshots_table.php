<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('screenshots', function (Blueprint $table) {
            $table->id();
            $table->text('url');
            $table->string('status')->default('pending'); // pending, processing, done, failed
            $table->string('file_path')->nullable();      // chemin MinIO une fois fait
            $table->boolean('full_size')->default(false);
            $table->timestamps();                         // created_at + updated_at
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('screenshots');
    }
};