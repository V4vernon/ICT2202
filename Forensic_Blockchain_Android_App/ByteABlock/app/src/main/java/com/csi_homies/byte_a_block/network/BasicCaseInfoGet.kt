package com.csi_homies.byte_a_block.network

import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Headers
import retrofit2.http.Query

interface BasicCaseInfoGet {
    /*
     After appending the query to the GET request, we would return Call, what it does is to use our
     data class WeatherResponse as a response to the whole query call. We want a WeatherResponse
     object (as a result, a GSON object) which will contain all the different information passed
     back to us, that we have laid out in the WeatherResponse data class
     */
    @Headers("Connection:Close")
    @GET("api/basic_case_info/")
    fun getBasicCaseInfo(
        @Query("username") username: String?,
        @Query("password") password: String?
    ): Call<BasicCaseInfoResponse>
}